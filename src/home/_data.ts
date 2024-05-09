// This sets the homepage to be / if the slug matches the version
export const url = (page) => {
  if (page.data.version === page.data.basename) return '/';
}

export const layout = 'layouts/simple.njk';