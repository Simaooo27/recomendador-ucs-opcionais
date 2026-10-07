// Mostra ou esconde a palavra-passe ao carregar no ícone de olho (ver templates/macros/password.html).
document.querySelectorAll("[data-toggle-password]").forEach(function (button) {
  var input = document.getElementById(button.dataset.togglePassword);
  if (!input) {
    return;
  }
  button.hidden = false;
  button.addEventListener("click", function () {
    var show = input.type === "password";
    input.type = show ? "text" : "password";
    button.setAttribute("aria-pressed", show ? "true" : "false");
    var label = show ? button.dataset.labelHide : button.dataset.labelShow;
    button.setAttribute("aria-label", label);
    button.title = label;
    input.focus();
  });
});
// Antes de enviar o formulário, volta a esconder (o navegador não guarda a palavra-passe como texto).
document.querySelectorAll("form").forEach(function (form) {
  form.addEventListener("submit", function () {
    form.querySelectorAll("[data-toggle-password]").forEach(function (button) {
      var input = document.getElementById(button.dataset.togglePassword);
      if (input) {
        input.type = "password";
      }
    });
  });
});
