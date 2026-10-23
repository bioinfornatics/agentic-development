/* Native disclosure and links work without JavaScript. Add dismissal and arrows. */
document.querySelectorAll('.language-selector').forEach((selector) => {
  const summary = selector.querySelector('summary');
  const links = [...selector.querySelectorAll('a')];
  selector.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      selector.open = false;
      summary.focus();
      event.preventDefault();
    } else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      selector.open = true;
      const index = links.indexOf(document.activeElement);
      const next = event.key === 'ArrowDown' ? (index + 1) % links.length : (index < 0 ? links.length - 1 : (index + links.length - 1) % links.length);
      links[next].focus();
      event.preventDefault();
    }
  });
  document.addEventListener('click', (event) => {
    if (!selector.contains(event.target)) selector.open = false;
  });
  selector.addEventListener('focusout', () => {
    setTimeout(() => { if (!selector.contains(document.activeElement)) selector.open = false; }, 0);
  });
});
