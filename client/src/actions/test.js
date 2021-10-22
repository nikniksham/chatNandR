import axios from 'axios'

export const test = async (some_data) => {
    try {
        const response = await axios.post("http://localhost:8000/api/test/" + some_data, {
            some_data
        })
        console.log(response.data.okay)
        alert(response.data.okay)
//        alert(response.data.message)
    } catch (e) {
        alert(e)
    }
}

export default test