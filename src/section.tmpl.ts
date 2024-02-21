export const layout ='layouts/section.njk';
export const tags = ['section'];

export default function*({ search }) {
  for (const report of search.pages('report')) {
    const {
      title: reportTitle,
      url,
      sections = [],
    } = report.data;

    // Iterate through the sections
    for (const section of sections) {
      const {
        title,
        read_more,
      } = section;

      if (read_more === undefined || read_more !== false) yield {
        url: `${url}${title.toLowerCase()}/`,
        reporttitle: `${reportTitle}`,
        report: url,
        ...section,
      }
    }  
  }
}