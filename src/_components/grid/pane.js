export const css = `
.auto-grid .pane {
  --max-height: unset;
  padding: 1rem;
  display: block;
  height: 100%;
  min-height: 20rem;
  color: inherit;
  max-height: var(--max-height);
  overflow-y: scroll;
}
.auto-grid .pane:hover, .auto-grid .pane:focus { background: #efefef; }
`;

export default function ({ content, link, tag = 'div', maxHeight = undefined }) {
  // let paneContent = content;
  // if (link) {
  //   paneContent = `<a href=${link} class='>${content}</a>`
  //   `
  // } else {
  //   body = 
  // }

  let style = '';
  if (maxHeight !== undefined)
    style = `style="--max-height: ${maxHeight};"`

  if ( link ) {
    return `
      <${tag}>
        <a class='pane'${style} href='${link}'>
          ${ content }
        </a>
      </${tag}>
    `;
  }

  return `
    <${tag} ${style} class='pane'>
      ${ content }
    </${tag}>
  `;



;
}