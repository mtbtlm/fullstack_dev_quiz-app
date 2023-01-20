export default {
      clear() {
            window.localStorage.clear();
      },
      savePlayerName(playerName) {
            window.localStorage.setItem("playerName", playerName);
      },
      getPlayerName() {
            return window.localStorage.getItem("playerName");
      },
      saveParticipationScore(participationScore) {
            window.localStorage.setItem("playerScore", participationScore);
      },
      getParticipationScore() {
            return window.localStorage.getItem("playerScore");
      },
      saveIdFromPos(id_pos) {
            window.localStorage.setItem("idFromPos", id_pos);
      },
      getIdFromPos() {
            return window.localStorage.getItem("idFromPos");
      }
};