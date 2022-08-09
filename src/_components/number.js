export const css = `
  .big-number {
    font-size: 3rem;
	line-height: 1.25em;
    text-align: center;
    border: none;
  }
`;

export default function({ number }) {
  return `
  <div class='big-number'>
    ${ number }
  </div>
`
}