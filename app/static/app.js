/* Interações das páginas (OptaBem).
 *
 * Tudo o que está aqui é um extra: sem JavaScript as páginas funcionam e mostram a
 * mesma informação. Quem pediu ao sistema menos animação não vê movimento.
 *
 *   1. Mapa interativo da página de apresentação (escolher um caminho), com o nome
 *      do caminho escrito à mão (as letras vêm de app/manuscrito.py)
 *   2. Linha de «Como funciona» que se desenha ao descer a página
 *   3. Regras da palavra-passe marcadas enquanto escreve (criar conta)
 *   4. Botões que mostram «a enviar» e evitam envios repetidos
 *   5. Números do painel de gestão que contam até ao valor
 */
(function () {
  "use strict";

  var menosMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Escrever à mão: o traço percorre cada contorno, por ordem, e no fim a tinta enche as letras. */
  function escrever(svg) {
    if (!svg || menosMovimento) return;
    var tracos = Array.prototype.slice.call(svg.querySelectorAll(".manuscrito-traco"));
    var tinta = svg.querySelector(".manuscrito-tinta");
    var duracao = 1.4; // segundos para a caneta atravessar a palavra
    var n = Math.max(1, tracos.length);
    tracos.forEach(function (traco) {
      var comprimento = traco.getTotalLength();
      traco.style.transition = "none";
      traco.style.strokeDasharray = comprimento;
      traco.style.strokeDashoffset = comprimento;
    });
    if (tinta) { tinta.style.transition = "none"; tinta.style.opacity = "0"; }
    // Dois frames: o primeiro fixa o início sem transição; o segundo arranca o desenho.
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () {
        tracos.forEach(function (traco, i) {
          var cada = (duracao / n) * 2.4;
          var inicio = 0.05 + (i / n) * duracao;
          traco.style.transition = "stroke-dashoffset " + cada.toFixed(3) + "s ease-out " + inicio.toFixed(3) + "s";
          traco.style.strokeDashoffset = "0";
        });
        if (tinta) {
          tinta.style.transition = "opacity 0.45s ease-out " + (0.05 + duracao * 0.72).toFixed(3) + "s";
          tinta.style.opacity = "1";
        }
      });
    });
  }

  /* 1. Mapa interativo ---------------------------------------------------- */
  document.querySelectorAll("[data-mapa]").forEach(function (mapa) {
    var controlos = mapa.querySelector("[data-mapa-controlos]");
    var porque = mapa.querySelector("[data-mapa-porque]");
    var botoes = Array.prototype.slice.call(mapa.querySelectorAll("[data-opcao]"));
    if (!controlos || !botoes.length) return;
    controlos.hidden = false;

    function escolher(indice) {
      mapa.setAttribute("data-ativo", String(indice));
      botoes.forEach(function (botao, i) {
        botao.setAttribute("aria-pressed", i === indice ? "true" : "false");
      });
      porque.textContent = botoes[indice].getAttribute("data-porque");
      mapa.querySelectorAll("[data-escrita-item]").forEach(function (item, i) {
        item.hidden = i !== indice;
        if (i === indice) escrever(item.querySelector("svg"));
      });
    }

    // Enquanto ninguém mexe, o mapa mostra os caminhos um a um.
    var automatico = null;
    function parar() {
      if (automatico) window.clearInterval(automatico);
      automatico = null;
    }
    botoes.forEach(function (botao, i) {
      botao.addEventListener("click", function () { parar(); escolher(i); });
    });
    mapa.addEventListener("pointerenter", parar);
    mapa.addEventListener("focusin", parar);

    escrever(mapa.querySelector('[data-escrita-item="0"] svg'));

    if (!menosMovimento) {
      var atual = 0;
      automatico = window.setInterval(function () {
        if (document.hidden) return;
        atual = (atual + 1) % botoes.length;
        escolher(atual);
      }, 4200);
    }
  });

  /* 2. Linha de «Como funciona» ------------------------------------------- */
  document.querySelectorAll("[data-passos]").forEach(function (lista) {
    if (menosMovimento) return; // a linha fica completa desde o início
    var passos = Array.prototype.slice.call(lista.children);
    lista.classList.add("passos-animados");
    var pedido = false;

    function atualizar() {
      pedido = false;
      var caixa = lista.getBoundingClientRect();
      var alvo = window.innerHeight * 0.6; // a linha acompanha 60% da altura do ecrã
      var progresso = Math.min(1, Math.max(0, (alvo - caixa.top) / caixa.height));
      lista.style.setProperty("--progresso", progresso.toFixed(3));
      passos.forEach(function (passo) {
        var meio = passo.offsetTop + 16;
        passo.classList.toggle("alcancado", progresso * caixa.height >= meio);
      });
    }
    function pedir() {
      if (!pedido) { pedido = true; window.requestAnimationFrame(atualizar); }
    }
    window.addEventListener("scroll", pedir, { passive: true });
    window.addEventListener("resize", pedir);
    atualizar();
  });

  /* 3. Regras da palavra-passe -------------------------------------------- */
  document.querySelectorAll("[data-regras]").forEach(function (lista) {
    var form = lista.closest("form");
    var campo = form && form.querySelector("#password");
    var repetir = form && form.querySelector("#password_confirm");
    if (!campo || !repetir) return;
    var minimo = parseInt(lista.getAttribute("data-minimo"), 10) || 8;
    lista.hidden = false;

    function marcar(regra, cumprida) {
      var item = lista.querySelector('[data-regra="' + regra + '"]');
      if (item) item.classList.toggle("cumprida", cumprida);
    }
    function verificar() {
      var valor = campo.value;
      marcar("tamanho", valor.length >= minimo);
      marcar("letra", /[A-Za-zÀ-ÿ]/.test(valor));
      marcar("numero", /[0-9]/.test(valor));
      marcar("iguais", valor.length > 0 && valor === repetir.value);
    }
    campo.addEventListener("input", verificar);
    repetir.addEventListener("input", verificar);
  });

  /* 4. Botões «a enviar» -------------------------------------------------- */
  document.querySelectorAll("form").forEach(function (form) {
    form.addEventListener("submit", function () {
      var botao = form.querySelector('button[type="submit"]');
      if (!botao) return;
      // Desativar depois de o pedido sair, para não o impedir.
      window.setTimeout(function () {
        botao.disabled = true;
        botao.classList.add("a-enviar");
        botao.setAttribute("aria-busy", "true");
      }, 0);
    });
  });
  // Ao voltar atrás no navegador, os botões voltam ao normal.
  window.addEventListener("pageshow", function () {
    document.querySelectorAll("button.a-enviar").forEach(function (botao) {
      botao.disabled = false;
      botao.classList.remove("a-enviar");
      botao.removeAttribute("aria-busy");
    });
  });

  /* 5. Números que contam ------------------------------------------------- */
  if (!menosMovimento) {
    document.querySelectorAll("[data-contar]").forEach(function (elemento) {
      var final = parseInt(elemento.getAttribute("data-contar"), 10);
      if (!(final > 0)) return;
      var inicio = null;
      var duracao = 700;
      function passo(agora) {
        if (inicio === null) inicio = agora;
        var t = Math.min(1, (agora - inicio) / duracao);
        var suave = 1 - Math.pow(1 - t, 3); // abranda no fim
        elemento.textContent = String(Math.round(final * suave));
        if (t < 1) window.requestAnimationFrame(passo);
      }
      elemento.textContent = "0";
      window.requestAnimationFrame(passo);
    });
  }
})();
