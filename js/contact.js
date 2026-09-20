/* The static portfolio composes email in the visitor's own email app. */
(function () {
  'use strict';
  var form = document.getElementById('email-form');
  if (!form) return;

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    if (!form.reportValidity()) return;
    var name = form.elements.namedItem('name').value.trim();
    var email = form.elements.namedItem('email').value.trim();
    var message = form.elements.namedItem('message').value.trim();
    var subject = 'Portfolio enquiry' + (name ? ' from ' + name : '');
    var body = 'Name: ' + name + '\r\nEmail: ' + email + '\r\n\r\n' + message;
    window.location.href = 'mailto:info@bransol.net?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
}());
