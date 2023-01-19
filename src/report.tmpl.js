export const layout = 'report.njk';

const conditionalReportFilter = ([_, report]) => report.draft !== true;

/**
 * Generator function which creates a page per report data object.
 * 
 * The report object appears as a object of report definitions defined with a key.
 * 
 * @param { reports:  } options
 */

export default function* ({ reports }) {
  for (const [reportSlug, report] of Object.entries(reports).filter(conditionalReportFilter)) {
    const url = `/reports/${reportSlug}/`;

    if (report.sections !== undefined ) {
      for (const [sectionIndex, section] of Object.entries(report.sections)) {
        if (section.read_more === undefined || section.read_more !== false) yield {
          url: `${url}${section.title}/`,
          reporttitle: `${report.title}`,
          report: url,
          layout: 'section.njk',
          tags: ['section'],
          index: sectionIndex,
          ...section,
        }
      }  
    }
    yield {
      url,
      tags: ['report'],
      ...report,
    }
  }
}