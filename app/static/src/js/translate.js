window.addEventListener('load', (event) => {
  const posts = document.querySelectorAll('[data-translate-post]');

  posts.forEach(post => {
    const trigger = post.querySelector('[data-translate-post-trigger]');
    trigger.addEventListener('click', (event) => {
      event.preventDefault();

      translate(post);
    });

  });
});

const translate = (post) => {
  const title = post.querySelector('[data-translate-post-title]');
  const body = post.querySelector('[data-translate-post-body]');
  const sourceLang = post.dataset.postLanguage;
  const destLang = post.dataset.postLocale;

  const url = `/translate`;
  const options = {
    method: 'POST',
    mode: 'cors',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      'text': [
        { 'text': title.innerHTML },
        { 'text': body.innerHTML }
      ],
      'source_language': sourceLang,
      'dest_language': destLang
    })
  };
  const r = new Request('/translate', options);

  fetch(r)
    .then(response => response.json())
    .then(data => {
      title.innerHTML = data['text'][0];
      body.innerHTML = data['text'][1];
    })
    .catch(err => console.log(err));
};
