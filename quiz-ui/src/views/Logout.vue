<script>
import adminStorageService from "@/services/AdminStorage";
export default{
    name: "logout",
    async created() {
        console.log("Composant logout 'created'")
        adminStorageService.clearToken()
        this.$router.push('/');
    }
}
</script>