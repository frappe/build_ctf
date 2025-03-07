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

// force open links in new tab
const defaultRender =
	markdown.renderer.rules.link_open ||
	function (tokens, idx, options, env, self) {
		return self.renderToken(tokens, idx, options)
	}

markdown.renderer.rules.link_open = function (tokens, idx, options, env, self) {
	tokens[idx].attrSet('target', '_blank')
	return defaultRender(tokens, idx, options, env, self)
}

const markdownContent = computed(() => {
	let content = props.content
	Object.keys(props.variables).forEach((key) => {
		content = content.replace(new RegExp(`{{${key}}}`, 'g'), props.variables[key])
	})
	return content
})
</script>
