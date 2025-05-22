import axios from 'axios'

export const getUser = () =>{
  const user_info = {}
  axios.get('https://demo-fast-api-lms.vercel.app/home_profile', {withCredentials: true}).then(function(response){
    console.log(response.data)
    user_info = response.data
    return { user_info }
  }).catch(
    function(error){
      console.log(error)
      if(error.response.status === 401)
        router.push({name:'Login'})
      else{
        console.log(error.response)
        return { error }
      }
    }
  )
}