<template>
	<div class="p-10">
		<ListView
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
import { ListView, createResource } from 'frappe-ui'
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

const openStageDialog = (stage) => {
	console.log(stage)
	selectedStage.value = stage
	showStageDialog.value = true
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
