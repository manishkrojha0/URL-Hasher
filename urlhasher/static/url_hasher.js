document.addEventListener("DOMContentLoaded", function(event) {
    const form = document.getElementById("utm-form");
    const utmUrl = document.getElementById("utm-url");
  
    form.addEventListener("submit", function(event) {
      event.preventDefault();
  
      const utmSource = document.getElementById("utm-source").value.trim();
      const utmMedium = document.getElementById("utm-medium").value.trim();
      const utmCampaign = document.getElementById("utm-campaign").value.trim();
      const utmContent = document.getElementById("utm-content").value.trim();
      const utmTerm = document.getElementById("utm-term").value.trim();
  
      const utmParams = {
        utm_source: utmSource,
        utm_medium: utmMedium,
        utm_campaign: utmCampaign,
        utm_content: utmContent,
        utm_term: utmTerm
      };
  
      const queryParams = new URLSearchParams(utmParams);
      const url = "https://example.com/?" + queryParams.toString();
  
      utmUrl.innerText = url;
      utmUrl.setAttribute("href", url);
      utmUrl.classList.remove("d-none");
    });
  });
  