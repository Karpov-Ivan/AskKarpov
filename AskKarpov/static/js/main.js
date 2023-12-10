function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const items_question = document.getElementsByClassName('like-section-question');

for (let item of items_question) {
    const [button_dislike, counter, button_like] = item.children;

    button_dislike.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('question_id', button_dislike.dataset.id)
        const csrfToken = getCookie('csrftoken');

        const request = new Request('/dislike-question', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.value = data.count;
            });

    })

    button_like.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('question_id', button_like.dataset.id)
        const csrfToken = getCookie('csrftoken');

        const request = new Request('/like-question', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.value = data.count;
            });
    })
}

const items_answer = document.getElementsByClassName('like-section-answer');

for (let item of items_answer) {
    const [button_dislike, counter, button_like] = item.children;

    button_dislike.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('answer_id', button_dislike.dataset.id)
        const csrfToken = getCookie('csrftoken');

        const request = new Request('/dislike-answer', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.value = data.count;
            });

    })

    button_like.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('answer_id', button_like.dataset.id)
        const csrfToken = getCookie('csrftoken');

        const request = new Request('/like-answer', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.value = data.count;
            });
    })
}

const items_answer_correct_check = document.getElementsByClassName('correct-section-answer');

for (let item of items_answer_correct_check) {
    const [correct_check, correct] = item.children;

    correct_check.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('answer_id', correct_check.dataset.id)
        const csrfToken = getCookie('csrftoken');

        const request = new Request('/correct-answer', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                correct.innerHTML = data.correct;
            });
    })
}