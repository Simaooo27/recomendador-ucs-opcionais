/* Interações das páginas (OptaBem).
 *
 * Tudo o que está aqui é um extra: sem JavaScript as páginas funcionam e mostram a
 * mesma informação. Quem pediu ao sistema menos animação não vê movimento.
 *
 *   1. Pesquisa de cursos da página de apresentação: resultados enquanto se escreve,
 *      com as fichas a deslizar para o novo lugar (e a nota «comece por aqui» escrita à mão)
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

  /* 1. Pesquisa de cursos ------------------------------------------------- */
  // Os resultados vêm de /cursos/pesquisa (Python, app/catalogo). Aqui só se desenham as
  // fichas: as que ficam deslizam para o novo lugar, as novas aparecem uma a uma.
  function semAcentos(texto) {
    return texto.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  // Põe <mark> à volta das palavras pesquisadas, sem mexer nos acentos do texto original.
  function realcar(elemento, texto, palavras) {
    elemento.textContent = "";
    if (!palavras.length) { elemento.textContent = texto; return; }
    var normal = "", mapa = [];
    for (var i = 0; i < texto.length; i++) {
      var letra = semAcentos(texto[i]);
      for (var j = 0; j < letra.length; j++) { normal += letra[j]; mapa.push(i); }
    }
    var marcas = new Array(texto.length).fill(false);
    palavras.forEach(function (palavra) {
      var desde = 0, pos;
      while (palavra && (pos = normal.indexOf(palavra, desde)) !== -1) {
        for (var k = pos; k < pos + palavra.length; k++) marcas[mapa[k]] = true;
        desde = pos + palavra.length;
      }
    });
    var atual = null, marcado = null;
    for (var n = 0; n < texto.length; n++) {
      if (marcas[n] !== marcado) {
        atual = marcas[n] ? document.createElement("mark") : document.createTextNode("");
        elemento.appendChild(atual);
        marcado = marcas[n];
      }
      if (atual.nodeType === 3) atual.appendData(texto[n]); else atual.textContent += texto[n];
    }
  }

  document.querySelectorAll("[data-procura]").forEach(function (procura) {
    var campo = procura.querySelector("[data-procura-campo]");
    var lista = document.querySelector("[data-cursos]");
    var modelo = document.querySelector("[data-modelo-curso]");
    var titulo = document.querySelector("[data-resultados-titulo]");
    var conta = document.querySelector("[data-resultados-conta]");
    var vazio = document.querySelector("[data-resultados-vazio]");
    if (!campo || !lista || !modelo || !window.fetch) return;

    var pedidoAtual = 0;
    var espera = null;

    function preencher(item, curso, palavras) {
      item.setAttribute("data-chave", curso.chave);
      item.querySelectorAll("[data-campo]").forEach(function (el) {
        var nome = el.getAttribute("data-campo");
        var valor = curso[nome];
        var semValor = valor === null || valor === undefined || valor === "";
        el.classList.toggle("sem-dados", semValor && el.hasAttribute("data-vazio"));
        if (semValor) {
          el.textContent = el.getAttribute("data-vazio") || "—";
        } else if (nome === "curso" || nome === "instituicao" || nome === "localidade") {
          realcar(el, String(valor), palavras);
        } else {
          el.textContent = String(valor);
        }
      });
      // Ligações da ficha: «Ver na DGES» (fonte) e o nome do curso (ficha completa, US05).
      item.querySelectorAll("[data-campo-href]").forEach(function (el) {
        var destino = curso[el.getAttribute("data-campo-href")];
        if (destino) el.href = destino;
      });
    }

    function mostrar(dados) {
      var palavras = semAcentos(dados.termo || "").split(/\s+/).filter(Boolean);
      // FLIP: guardar onde estava cada ficha antes de mudar a lista.
      var antes = {};
      lista.querySelectorAll("[data-chave]").forEach(function (el) {
        antes[el.getAttribute("data-chave")] = el.getBoundingClientRect();
      });
      var existentes = {};
      lista.querySelectorAll("[data-chave]").forEach(function (el) { existentes[el.getAttribute("data-chave")] = el; });

      var novas = [];
      var fragmento = document.createDocumentFragment();
      dados.cursos.forEach(function (curso) {
        var item = existentes[curso.chave];
        if (!item) {
          item = modelo.content.firstElementChild.cloneNode(true);
          novas.push(item);
        }
        preencher(item, curso, palavras);
        fragmento.appendChild(item);
      });
      lista.textContent = "";
      lista.appendChild(fragmento);

      // Títulos e mensagens.
      if (dados.amostra) {
        titulo.textContent = lista.getAttribute("data-texto-amostra");
        conta.textContent = "";
      } else {
        titulo.textContent = lista.getAttribute("data-texto-encontrados").replace("{termo}", dados.termo);
        conta.textContent = dados.total
          ? lista.getAttribute("data-texto-conta").replace("{mostrados}", dados.cursos.length).replace("{total}", dados.total)
          : "";
      }
      vazio.hidden = dados.cursos.length > 0 || dados.amostra;
      vazio.textContent = lista.getAttribute("data-texto-vazio").replace("{termo}", dados.termo);

      if (menosMovimento || !lista.animate) return;
      // As que já existiam deslizam da posição antiga para a nova.
      lista.querySelectorAll("[data-chave]").forEach(function (el) {
        var antiga = antes[el.getAttribute("data-chave")];
        if (!antiga || novas.indexOf(el) !== -1) return;
        var nova = el.getBoundingClientRect();
        var dx = antiga.left - nova.left, dy = antiga.top - nova.top;
        if (dx || dy) {
          el.animate([{ transform: "translate(" + dx + "px," + dy + "px)" }, { transform: "none" }],
                     { duration: 420, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)" });
        }
      });
      // As novas aparecem uma a uma.
      novas.forEach(function (el, i) {
        el.animate([{ opacity: 0, transform: "translateY(14px) scale(0.98)" }, { opacity: 1, transform: "none" }],
                   { duration: 360, delay: Math.min(i, 8) * 45, easing: "cubic-bezier(0.2, 0.8, 0.2, 1)", fill: "backwards" });
      });
    }

    function pesquisar(termo) {
      var numero = ++pedidoAtual;
      fetch("/cursos/pesquisa?q=" + encodeURIComponent(termo), { headers: { Accept: "application/json" } })
        .then(function (resposta) { return resposta.ok ? resposta.json() : null; })
        .then(function (dados) {
          if (!dados || numero !== pedidoAtual) return; // chegou uma resposta mais recente
          mostrar(dados);
          var endereco = termo ? "?q=" + encodeURIComponent(termo) : window.location.pathname;
          window.history.replaceState(null, "", endereco);
        })
        .catch(function () { /* sem rede: fica o que estava */ });
    }

    campo.addEventListener("input", function () {
      window.clearTimeout(espera);
      espera = window.setTimeout(function () { pesquisar(campo.value.trim()); }, 160);
    });
    campo.form.addEventListener("submit", function (evento) {
      evento.preventDefault();
      pesquisar(campo.value.trim());
      document.getElementById("resultados").scrollIntoView({ behavior: menosMovimento ? "auto" : "smooth" });
    });
    procura.querySelectorAll("[data-termo]").forEach(function (ligacao) {
      ligacao.addEventListener("click", function (evento) {
        evento.preventDefault();
        campo.value = ligacao.getAttribute("data-termo");
        pesquisar(campo.value);
        campo.focus();
      });
    });

    escrever(procura.querySelector(".procura-nota svg.manuscrito"));
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
