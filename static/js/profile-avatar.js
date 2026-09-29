document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("id_avatar");
  const preview = document.getElementById("avatar-preview-image");

  if (!input || !preview) {
    return;
  }

  input.addEventListener("change", () => {
    const [file] = input.files;
    if (!file) {
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    preview.src = objectUrl;
    preview.addEventListener("load", () => URL.revokeObjectURL(objectUrl), { once: true });
  });
});
