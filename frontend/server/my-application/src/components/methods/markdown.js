import { marked } from 'marked'

export const reloadMathJax = () => {
  window.MathJax.typesetPromise()
}
export const markdownToHtml = (md) => marked(md)
