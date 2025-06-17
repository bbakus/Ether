import { useNavigate } from "react-router-dom"
import '../styles/Home.css'



function Home(){

    const navigate = useNavigate()

    function handleReading(){
        navigate('/spread')
    }

    return(

        <div>
            <img className='home-background' src='/images/home_background.png'/>
            <div className='header'>
                <h1 className='home-title'>ETHER</h1>
            </div>
            <button onClick={handleReading} className='enter-button'>ENTER</button>

        </div>
    )


}


export default Home