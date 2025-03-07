<template>
	<div class="prose-f" v-html="markdown.render(markdownContent)"></div>
</template>
<script setup>
import MarkdownIt from 'markdown-it'
import MarkdownItAbbr from 'markdown-it-abbr'
import MarkdownItAnchor from 'markdown-it-anchor'
import MarkdownItFootnote from 'markdown-it-footnote'
import MarkdownItHighlightjs from 'markdown-it-highlightjs'
import MarkdownItSub from 'markdown-it-sub'
import MarkdownItSup from 'markdown-it-sup'
import { computed } from 'vue'

const markdown = new MarkdownIt({
	html: true,
	typographer: true,
})
	.use(MarkdownItAbbr)
	.use(MarkdownItAnchor)
	.use(MarkdownItFootnote)
	.use(MarkdownItHighlightjs)
	.use(MarkdownItSub)
	.use(MarkdownItSup)

const props = defineProps({
	content: {
		type: String,
		default: '',
	},
	variables: {
		type: Object,
		default: {},
	},
})

const markdownContent = computed(() => {
	let content = props.content
	Object.keys(props.variables).forEach((key) => {
		content = content.replace(new RegExp(`{{${key}}}`, 'g'), props.variables[key])
	})
	return content
})
</script>
