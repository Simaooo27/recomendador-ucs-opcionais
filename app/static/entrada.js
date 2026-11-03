/* Entrada suave do OptaBem (revisão de 03/11).
 *
 * Corre no <head>, antes de a página ser desenhada: na primeira página de cada visita põe a
 * classe «primeira-entrada» no <html>, e o style.css (secção 14) faz o conteúdo aparecer com um
 * desvanecer curto. As páginas seguintes da mesma visita abrem logo, sem esperar.
 * Fica num ficheiro próprio porque a política de segurança (app/security.py) não deixa correr
 * JavaScript escrito dentro da página.
 */
try {
  if (!window.sessionStorage.getItem("optabem-entrou")) {
    document.documentElement.classList.add("primeira-entrada");
    window.sessionStorage.setItem("optabem-entrou", "1");
  }
} catch (erro) {
  /* Sem sessionStorage (ex.: navegação privada muito restrita): a página abre sem animação. */
}
