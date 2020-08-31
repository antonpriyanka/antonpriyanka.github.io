  const catElement = document.getElementById('cat');
  if (catElement.complete && catElement.naturalHeight !== 0) {
    catElement.style.display = '';
  } else {
    catElement.onload = () => {
      catElement.style.display = '';
    }
  }
