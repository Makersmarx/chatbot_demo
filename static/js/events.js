// Just test for submit button

const submit = document.querySelector('.submit');
const message = document.querySelector('.messages');

const sayHello = () => {
  message.textContent = 'Team Chicago will Own this $%@%^';
};

submit.addEventListener('click', sayHello);
