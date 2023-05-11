export const css = `
.auto-grid .pane {
  --max-height: unset;
  padding: 0rem;
  display: block;
  height: 100%;
  min-height: 10rem;
  color: inherit;
  background: #fceee7;  
  text-align: left;
}
.auto-grid .pane:hover, .auto-grid .pane:focus { background: #efefef; }
`;

export default function ({ content, link, tag = 'div', maxHeight = undefined, extra_classes = 'grey-bg', rows = undefined, columns = undefined }) {
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

  if (rows !== undefined)
    style = `style="grid-row:auto/span ${ rows };"`

  if (columns !== undefined)
    style = `style="grid-column:span ${ columns };"`

  if ( link ) {
    return `
      <${tag}>
        <a class='pane ${extra_classes}'${style} href='${link}'>
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