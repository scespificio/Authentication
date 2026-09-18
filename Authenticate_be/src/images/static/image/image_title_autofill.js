// Remplit #id_title avec le nom du fichier choisi (sans extension) si le champ est vide
document.addEventListener("DOMContentLoaded", function () {
  const fileInput  = document.getElementById("id_image_file");
  const titleInput = document.getElementById("id_title");

  if (!fileInput || !titleInput) return;

  function filenameToTitle(name) {
    // retire l'extension
    let base = name.split(".").slice(0, -1).join(".");
    // nettoyages simples : remplace _ et - par des espaces, trim
    base = base.replace(/[_-]+/g, " ").trim();
    // capitalise la première lettre (optionnel)
    if (base) base = base[0].toUpperCase() + base.slice(1);
    return base;
  }

  fileInput.addEventListener("change", function () {
    if (titleInput.value) return; // ne pas écraser un titre déjà saisi
    if (fileInput.files && fileInput.files.length > 0) {
      titleInput.value = filenameToTitle(fileInput.files[0].name);
    } else if (fileInput.value) {
      // fallback (certains navigateurs remplissent value avec le chemin)
      const parts = fileInput.value.split(/[\\/]/);
      titleInput.value = filenameToTitle(parts[parts.length - 1]);
    }
  });
});
