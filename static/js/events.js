// Just test for submit button
const text = document.getElementById('message-text');
const mapInfo = document.getElementById('mapInfo');

// test and grab users location, ping free api to convert lat/lon
const gridOne = document.querySelector('.gridOne');

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    gridOne.innerHTML = 'Geolocation is not supported by this browser.';
  }
};

// Show users city/zipcode in first grid block
const showPosition = async (position) => {
  const response = await fetch(
    `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}&localityLanguage=en`
  );
  const places = await response.json();
  mapInfo.innerHTML =
    'City: ' + places.locality + '<br>Zipcode: ' + places.postcode;
};

getLocation();

text.innerHTML.replace(/\*/g, '').trim();
