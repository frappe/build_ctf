<template>
	<Dialog v-bind:modelValue="showDialog" @update:modelValue="updateShowDialog">
		<template #body-title>
			<h3>{{ stage.title }}</h3>
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
					modelValue=""
				/>
				<Button variant="solid" class="w-full"> Submit Flag </Button>
			</div>
		</template>
	</Dialog>
</template>
<script setup>
import { TextInput, Dialog } from 'frappe-ui'
import MarkdownRenderer from './MarkdownRenderer.vue'

defineProps({
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
</script>
