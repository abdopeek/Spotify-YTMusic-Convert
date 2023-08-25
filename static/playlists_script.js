const confirmBtn = document.querySelector('.confirmBtn')
const playlists = document.querySelectorAll('.music-content');
let id;

playlists.forEach(function (playlist) {
    playlist.addEventListener('click', handleClick)})

function handleClick(e) {
    playlists.forEach(function(playlist) {
        playlist.classList.remove('active');
    })
    const clickedElement = e.target;
    if (clickedElement.classList.contains("music-content")) {
        parent.classList.toggle('active')
        let right = clickedElement.querySelector('.right');
        id = right.querySelector('.id').textContent;
        confirmBtn.value = id;
        console.log(id);
        e.stopPropagation()
    }
    else {
        let parent = clickedElement.closest(".music-content");
        parent.classList.toggle('active')
        let right = parent.querySelector('.right');
        id = right.querySelector('.id').textContent;
        confirmBtn.value = id;
        console.log(id);
        e.stopPropagation()
    }
}

