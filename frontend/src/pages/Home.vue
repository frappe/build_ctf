<template>
	<div class="p-5 w-screen">
		<div class="w-full flex flex-row justify-between items-center pb-5">
			<div>👋 Hi, {{ statusResource?.data?.full_name }}</div>
			<Button iconLeft="log-out" @click="logout" v-if="statusResource.data.logged_in"
				>Logout</Button
			>
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
				},
				{
					label: 'Status',
					key: 'status',
					width: '200px',
					align: 'center',
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
			:refreshStageList="() => stagesResource.reload()"
		/>
	</div>
</template>

<script setup>
import { ListView, createResource, Spinner } from 'frappe-ui'
import { computed, onMounted, ref } from 'vue'
import StageDialog from '../components/StageDialog.vue'

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
