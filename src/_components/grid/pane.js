export const css = `
.pane {
  padding: 1rem;
  display: block;
  height: 100%;
  min-height: 20rem;
  color: inherit;
}
.pane:hover, .pane:focus { background: #efefef; }
`;

export default function ({ content, link, tag = 'div' }) {
  // let paneContent = content;
  // if (link) {
  //   paneContent = `<a href=${link} class='>${content}</a>`
  //   `
  // } else {
  //   body = 
  // }

  if ( link ) {
    return `
      <${tag}>
        <a class='pane' href='${link}'>
          ${ content }
        </a>
      </${tag}>
    `;
  }

  return `
    <${tag} class='pane'>
      ${ content }
    </${tag}>
  `;



;
}