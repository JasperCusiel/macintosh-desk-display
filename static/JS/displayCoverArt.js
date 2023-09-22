let prevAlbumArtUrl = ""; // Declare the variable outside the function
function updateImage() {
  fetch("/currently_playing_info")
    .then((response) => response.json())
    .then((data) => {
      const artistName = data.artist_name;
      const songTitle = data.song_title;
      const albumName = data.album_name;
      const length = data.length;
      const progress = data.progress;
      const albumArtUrl = data.album_art_url;
      if (prevAlbumArtUrl !== albumArtUrl) {
        // Use the values to update the UI
        document.getElementById("artist").innerText = artistName;
        document.getElementById("track").innerText = songTitle;
        document.getElementById("album").innerText = albumName;

        const albumArt = document.getElementById("album-art");
        const albumBackground = document.getElementById("album-art-background");

        // albumBackground.style.backgroundImage = `url(${albumArtUrl})`;

        albumArt.style.opacity = 0; // Fade out the current image
        albumBackground.style.opacity = 0;
        albumArt.addEventListener("transitionend", () => {
          // albumBackground.style.backgroundImage = `url(${albumArtUrl})`;
          albumArt.src = albumArtUrl; // Update the image source
          albumArt.onload = () => {
            albumArt.style.opacity = 1; // Fade in the new image
            albumBackground.style.opacity = 1;
          };
          albumArt.src = albumArtUrl; // Update the image source
        });
      }
      prevAlbumArtUrl = albumArtUrl;
    });
}

// Call the updateImage function every 5 seconds
setInterval(updateImage, 5000);
