<template>
	<Badge
		variant="subtle"
		:ref_for="true"
		:theme="themeMap[status]"
		size="sm"
		:label="status"
		v-if="status"
	>
		{{ status }}
	</Badge>

</template>
<script setup>
import { Badge } from 'frappe-ui'
defineProps({
	status: {
		type: String,
		required: true,
	},
})

const themeMap = {
	'Not Attempted': 'gray',
	'Correct Flag': 'green',
	'Incorrect Flag': 'red',
}
</script>
