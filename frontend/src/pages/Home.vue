<template>
	<div class="p-5 w-screen">
		<div class="w-full flex flex-row justify-between items-center pb-5">
			<div>👋 Hi, {{ statusResource?.data?.full_name }}</div>
			<div v-if="statusResource.data.logged_in" class="flex flex-row gap-2 items-center">
				<p class="text-ink-gray-8 text-base h-min">
					Points -
					<span class="text-ink-gray-9 font-semibold">{{
						statusResource?.data?.total_points
					}}</span>
				</p>
				<a href="/leaderboard" target="_blank">
					<Button :iconLeft="ChartNoAxesColumn">Leaderboard</Button>
				</a>
				<Button iconLeft="log-out" @click="logout">Logout</Button>
			</div>
		</div>
		<div
			class="h-[80vh] min-w-full flex justify-center items-center"
			v-if="statusResource.data.logged_in && !statusResource.data.setup_completed"
		>
			<div class="flex flex-row gap-2 text-gray-900">
				<Spinner class="w-4" /> Setting Up CTF Stages
			</div>
		</div>
		<ListView
			v-if="statusResource.data.setup_completed"
			:columns="[
				{
					label: 'Stage',
					key: 'name',
					width: '100px',
				},
				{
					label: 'Title',
					key: 'title',
				},
				{
					label: 'Points',
					key: 'points',
					width: '100px',
					align: 'center',
					getLabel: ({ row }) => {
						return `${row.points} / ${row.max_points}`
					},
				},
				{
					label: 'Status',
					key: 'status',
					width: '150px',
					align: 'center',
					// hacky way to show the badge
					prefix: ({ row }) => {
						return h(StageStatusBadge, {
							// Show status badge
							status: row.status,
						})
					},
					getLabel: ({ row }) => {
						// Show blank label
						return ''
					},
				},
			]"
			:rows="stages"
			:options="{
				onRowClick: (row) => openStageDialog(row),
				selectable: false,
				showTooltip: true,
				resizeColumn: true,
				emptyState: {
					title: 'No Stages',
					description: 'Please wait to publish CTF Stages',
				},
			}"
			row-key="id"
		>
		</ListView>
		<StageDialog
			:stage="selectedStage"
			:showDialog="showStageDialog"
			@update:showDialog="(e) => (showStageDialog = e)"
			:refreshStageList="
				() => {
					stagesResource.reload()
					statusResource.reload()
				}
			"
		/>
	</div>
</template>

<script setup>
import { ListView, createResource, Spinner } from 'frappe-ui'
import { computed, h, onMounted, ref } from 'vue'
import StageDialog from '../components/StageDialog.vue'
import StageStatusBadge from '../components/StageStatusBadge.vue'
import ChartNoAxesColumn from '../assets/ChartNoAxesColumn.vue'

const showStageDialog = ref(false)
const selectedStage = ref({})
const stagesResource = createResource({
	url: '/api/method/ctf.api.stages',
	auto: true,
	method: 'GET',
	initialData: [],
})
const stages = computed(() => stagesResource?.data ?? [])

const statusResource = createResource({
	url: '/api/method/ctf.api.status',
	auto: true,
	method: 'GET',
	initialData: {},
	onSuccess: (data) => {
		if (data.logged_in) {
			if (data.setup_completed) {
				if (stages.value.length === 0) {
					stagesResource.reload()
				}
			} else {
				setTimeout(() => {
					statusResource.reload()
				}, 2000)
			}
		}
	},
})

const openStageDialog = (stage) => {
	selectedStage.value = stage
	showStageDialog.value = true
}

const logout = () => {
	fetch('/api/method/logout').then(() => {
		window.location.href = '/'
	})
}

onMounted(() => {
	const baseUrl = window.location.origin
	console.log(
		'👋 Hi, Welcome to Frappe Build CTF! 🚀\n\n' +
			'You might be looking for the registration link.\n\n' +
			'🔗 Visit: ' +
			baseUrl +
			'/frontend/cBSZTcX5OScQtKOScyahY9o3ShRcWDK6VqlBJl6CV2ZtB to register for the CTF',
	)
})
</script>
