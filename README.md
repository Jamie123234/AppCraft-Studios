# AppCraft Studios - Static Website

This repository contains the code for the AppCraft Studios static website. It's a single-page application built purely with HTML, Tailwind CSS (via CDN), and vanilla JavaScript for navigation.

## Description

AppCraft Studios is presented as a modern, responsive website showcasing services related to mobile and web application development. This implementation uses a single HTML file to simulate a multi-page experience by dynamically showing and hiding content sections based on user navigation (using URL hashes).

## Features

* **Single-Page Application (SPA) Feel:** Uses JavaScript to navigate between Home, Services, and Contact sections without page reloads.
* **Responsive Design:** Adapts to different screen sizes using Tailwind CSS utility classes.
* **Clean UI:** Modern design aesthetic with gradient buttons and clear typography.
* **Sections:**
    * **Home:** Hero section with a prominent heading, description, and call-to-action buttons.
    * **Services:** Detailed cards outlining various development services offered.
    * **Contact:** Contact form (static demo) and contact information.
    * **Privacy Policy & Terms of Service:** Placeholder pages linked from the footer.
* **Hash-Based Routing:** Uses URL fragments (`#home`, `#services`, etc.) for navigation and bookmarking specific sections.

## Technologies Used

* **HTML5:** Structure of the website.
* **Tailwind CSS (v3 via CDN):** Utility-first CSS framework for styling and layout.
* **Vanilla JavaScript:** For handling navigation logic (showing/hiding sections) and basic form interaction simulation.
* **Lucide Icons (via CDN/SVG):** For iconography.
* **Google Fonts (Inter):** For typography.

## Setup & Usage

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```
2.  **Open the file:** Simply open the `index.html` file in your web browser. No server or build process is required.

    * On macOS: `open index.html`
    * On Windows: `start index.html`
    * On Linux: `xdg-open index.html`

## Contact Form Note

The contact form included is for demonstration purposes only. As this is a static site, the form **does not actually send emails** out of the box. To make it functional, you would need to integrate it with a backend service or a third-party form handling service like:

* [Formspree](https://formspree.io/)
* [Netlify Forms](https://www.netlify.com/products/forms/)
* [Getform](https://getform.io/)
* A custom backend endpoint

The current JavaScript only simulates a "message sent" confirmation.

## License

Consider adding a license file (e.g., MIT License) to define how others can use your code.

---

*Crafted by AppCraft Studios*

  @media print {
    .ms-editor-squiggler {
        display:none !important;
    }
  }
  .ms-editor-squiggler {
    all: initial;
    display: block !important;
    height: 0px !important;
    width: 0px !important;
  }