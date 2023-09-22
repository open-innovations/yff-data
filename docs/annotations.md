# Annotations

Annotations are temporary additions to the content on the site.
The primary purpose for these is to allow YFF staff to provide additional narrative on the release of new figures, but conceptually they could be used for any additional content.

Each annotation has the following fields:

* **Annotation content** (`content`)  
  The annotation to display on the page.
  This field accepts markdown formatting.
  Ideally it should contain no headings.
  The top level of heading, if included, should be level 3.
* **Annotated page** (`refers_to`)  
  The full path of a page to which the annotation refers.
  Not all pages implement display of annotation.
* **First day for annotation** (`start_date`)  
  The first day on which the annotation should be shown.
* **Last day for annotation** (`end_date`)  
  The last day on which the annotation should be shown.
  This is optional, so can be ommitted, or entered as an empty string `''` if the annotation is not to end.
  
Each time the site is built, the pages implementing annotation display check if the annotations are to be displayed.
These are rendered in `start_date` order.

## Creating new annotations

There are two ways to manage annotations, via the headless content management system, and directly in the repository.

### Via the Content Management System

The site implements a headless Content Management System based on [Decap CMS](https://decapcms.org/) (formerly Netlify CMS).
To use this, you will need a GitHub account, and for that account to have edit access to the [yff-data GitHub repository](https://github.com/open-innovations/yff-data).

1.  Visit [the admin page](https://data.youthfuturesfoundation.org/admin/) for the Data Dashboard.
2.  If you are not logged in, you will need to click the **Login with GitHub**.
    This might ask you to log in to GitHub, if not already done.
    The first time you visit the site it will also ask permission to access your GitHub account details.
    This is required to get data from the GitHub repository and to add or update repository content.
3.  Once signed in you should see a list of collections including one called _Annotations_.
    Select this collection.
4.  You will be presented with a list of annotations, summarised by the document they
    refer to, and start and end dates.
    You can either select an existing annotation to edit it, or click the **New Annotation** button to create a new one.
5.  Edit the fields as required and click the **Publish** button / dropdown.
    This will present a few options related to publishing. Select the appropriate one.
    The app will attempt to save your changes and display a message stating success or failure.

Note that the site will then be updated and deployed. This can take a few minutes, after which point the site should be updated as required.

### Manual creation of annotations

1.  Create a new `.yml` file in the `src/_data/annotations/` directory.
    Filename is not important.
    The CMS-created files have a name derived from the creation time of the file in the format `YYYYMMDDThhmmss` (i.e. ISO 8601 full basic format).
2.  Add the following content and customise accordingly:
    ```yaml
    relates_to: <full repo path to annotated page>
    start_date: <first date for annotation
    end_date: <optional last date for annotation>
    content: |-
        A multi-line content string.
        
        * Will be _processed_ as **markdown**.
        
        NB blank lines must include the appropriate
        YAML spacing at the start.
    ```
3. Rebuild the site. If the page linked to by the `relates_to` field is designed to handle the annotations, they will be rendered.

## Implementation 

Annotations are stored as separate `.yml` files in the `src/_data/annotations/` folder in the GitHub repository.
Lume will make these available as the `annotations` context object.

### `get_annotations` filter

The `get_annotations` filter selects annotations relevant to the current page, and where the current date falls between the start and end.

The `annotations` in the Lume shared data context is an object: the filter converts this into an array which can be iterated as follows:

```html
{% for annotation in my_annotations %}
<div class='annotation'>
{{ annotation.content | md | safe }}
</div>
{% endfor %}
```

TODO Consider converting this into a tag or other helper?

### Decap CMS configuration

The Decap CMS configuration is managed per the [Netlify CMS plugin instructions](https://lume.land/plugins/netlify_cms/).

Two collections have been created

* Annotations
* Annotation targets (hidden)

The latter is used as a reference for the _Annotated page (`refers_to`)_ field.

Site pages are included in this collection if they meet the following criteria:

1. Filetype is `.njk`
2. Has a `title` attribute
3. Has a `tags` array which contains the `annotatable` value.

The `title` and `tags` attributes must be set in the page file itself, rather than in shared data associated with the page, i.e. in a `_data.*` or file in a `_data/` directory.
