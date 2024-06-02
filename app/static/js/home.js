document.addEventListener('DOMContentLoaded', function () {
    var preElement = document.querySelector('.pre-reader pre');
    var content = preElement.innerHTML;

    // Define the citation pattern
    var citationPattern = /\[([^\]]+)\]/g;

    // Use a regular expression to replace citations with underlined version
    var formattedContent = content.replace(citationPattern, function(_, p1) {
        return '<u>[' + p1 + ']</u>';
    });

    // Update the content of the pre element
    preElement.innerHTML = formattedContent;
});
