<template>
	<Dialog v-bind:modelValue="showDialog" @update:modelValue="updateShowDialog">
		<template #body-title>
			<h3>{{ stage.title }}&nbsp;&nbsp;<StageStatusBadge :status="stage_info.status" /></h3>
		</template>
		<template #body-content>
			<MarkdownRenderer
				:content="stage?.description ?? ''"
				:variables="stage?.variables ?? []"
			/>
		</template>
		<template #actions v-if="stage?.show_input">
			<div class="flex flex-col gap-2">
				<p class="text-base font-medium leading-6 text-gray-900">Enter Flag</p>
				<TextInput
					type="text"
					:ref_for="true"
					size="sm"
					variant="subtle"
					placeholder="FLAG{some_random_characters}"
					:disabled="false"
					v-model="stage_info.flag"
					@keydown="() => (stage_info.status = '')"
				/>
				<div
					v-if="stage_info.status"
					class="flex items-center rounded-md border px-2.5 py-2"
					:class="{
						'border-red-200 bg-red-100': !stage_info.correct,
						'border-green-200 bg-green-100': stage_info.correct,
					}"
				>
					<div class="text-p-sm font-medium text-gray-800">
						{{
							stage_info.correct
								? '🎉 You got the flag!'
								: 'Submitted flag is wrong. Retry !'
						}}
					</div>
				</div>
				<Button
					variant="solid"
					class="w-full"
					@click="submitFlag.submit"
					:loading="submitFlag.loading"
					loading-text="Submitting..."
				>
					Submit Flag
				</Button>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { TextInput, Dialog, createResource } from 'frappe-ui'
import MarkdownRenderer from './MarkdownRenderer.vue'
import { reactive, watch } from 'vue'
import StageStatusBadge from './StageStatusBadge.vue'
import { toast } from 'vue-sonner'

const props = defineProps({
	stage: {
		type: Object,
		required: true,
	},
	showDialog: {
		type: Boolean,
		required: true,
	},
	refreshStageList: {
		type: Function,
		required: true,
	},
})

const emit = defineEmits(['update:showDialog'])
const updateShowDialog = (value) => {
	emit('update:showDialog', value)
}

const stage_info = reactive({
	flag: '',
	correct: false,
	status: '',
})

watch(
	() => props.showDialog,
	(value) => {
		// Reset the stage_info when the dialog is closed
		if (!value) {
			stage_info.flag = ''
			stage_info.correct = false
			stage_info.status = ''
		} else {
			if (!props.stage?.submitted_flag) {
				return
			}
			stage_info.correct = props.stage.correct
			stage_info.flag = props.stage.submitted_flag
			stage_info.status = props.stage.status
		}
	},
)

const submitFlag = createResource({
	url: '/api/method/ctf.api.submit_flag',
	makeParams: () => ({
		stage: props.stage.name,
		flag: stage_info.flag,
	}),
	onSuccess: (data) => {
		stage_info.flag = data.submitted_flag
		stage_info.status = data.status
		stage_info.correct = data.correct
		props.refreshStageList()
		if (stage_info.correct) {
			toast.success('You got the flag! 🎉')
			setTimeout(() => {
				updateShowDialog(false)
			}, 1000)
		}
	},
})
</script>
