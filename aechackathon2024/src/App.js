import './App.css';
import {APIProvider, Map, MapCameraChangedEvent, AdvancedMarker,Pin } from '@vis.gl/react-google-maps';
import { useState } from 'react';
import {
  Button,
  Form,
  FormGroup,
  Label,
  Container,
  Row,
  Col,
  Input
} from 'reactstrap'

function App() {
  const [ price, setPrice ] = useState('')
  const [ address, setAddress ] = useState('')
  const [ city, setCity ]= useState('')
  const [ stateAbr, setStateAbr ]= useState('')
  const [ zip, setZipCode ] = useState('90017')
  const [ propertyType, setPropertyType ] = useState('')
  const [ latitude, setLatitude ] = useState(34.052913)
  const [ longitude, setLongitude ] = useState(-118.264340)
  const [  posits1, setPosits1  ] = useState([])
  const [  posits2, setPosits2  ] = useState([])
  const [  posits3, setPosits3  ] = useState([])
  const [  posits4, setPosits4  ] = useState([])
  const [  posits5, setPosits5  ] = useState([])

  const [ priceDisplay, setPriceDisplay ] = useState('')


  const submit = async (e) =>{
    e.preventDefault();

    let addressString = address.split(" ").join("+") + "+" + city.split(" ").join("+") + "+" + stateAbr.split(" ").join("+") + "+" + zip.split(" ").join("+")

    console.log(addressString)

    const googleMapResponse = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${addressString}&key=AIzaSyBR4OUYOMC4iSFYayAdkfgjfc_itpVDGfA`, {
      method: 'GET'
    });

    const googleMapData = await googleMapResponse.json();
    let lat, lng;

    if (googleMapData.status === 'OK'){
      let location = googleMapData.results[0].geometry.location
      lat = location.lat
      lng = location.lng
    }
    
    setLatitude(lat)
    setLongitude(lng)

    const response = await fetch('http://127.0.0.1:5000/rank-areas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        lat,
        lng,
        zip, 
        price, 
        propertyType
      })
    });

    const data = await response.json();
    if (data.status === 'success') {

      //const rankedAreas = data.data;
      const rankedAreas = [

        {price: 234442, lat: 34.039378, lng: -118.266300 },
        {price: 345344, lat: 34.028331, lng: -118.354338 },
        {price: 456545, lat: 34.028887, lng: -118.317183  },
        {price: 567567, lat: 34.049841, lng: -118.338460 },
        {price: 234234, lat: 34.066379, lng: -118.309870},
      ]

      // Update the positions based on the API response
      setPosits1([rankedAreas[0]])
      setPosits2([rankedAreas[1]])
      setPosits3([rankedAreas[2]])
      setPosits4([rankedAreas[3]])
      setPosits5([rankedAreas[4]])

      console.log('Ranked Areas:', rankedAreas);
    } else {
      console.error('There is Error:', data.message);
    }

  };


  return (<div className="App">
      <h1 id ="title">Find Your Zip Code
      </h1>
      <Container >
        <Row className="justify-content-center">
            <Form className="p-4" id="initial-form" onSubmit={submit} >
              <FormGroup row>
                <Label htmlFor="price" check>Price</Label>
                <Col sm={10}>
                  <Input type="number" name="price" id="price" placeholder="Enter your price" value={price} onChange={(e) => setPrice(e.target.value)} />
                </Col>
              </FormGroup>

              <FormGroup row>
                <Label htmlFor="address">Street Address</Label>
                <Col sm={10}>
                  <Input type="text" name="address" id="address" placeholder="What is your Street?" value={address} onChange={(e) => setAddress(e.target.value)}  />
                </Col>
              </FormGroup>

              <FormGroup row>
                <Label htmlFor="city">City</Label>
                <Col sm={10}>
                  <Input type="text" name="city" id="city" placeholder="What is your City?" value={city} onChange={(e) => setCity(e.target.value)}  />
                </Col>
              </FormGroup>

              <FormGroup row>
                <Label htmlFor="stateAbr">State</Label>
                <Col sm={10}>
                  <Input type="text" name="stateAbr" id="stateAbr" placeholder="What is your State?" value={stateAbr} onChange={(e) => setStateAbr(e.target.value)}  />
                </Col>
              </FormGroup>
              <FormGroup row>
                <Label htmlFor="zip">Zip Code</Label>
                <Col sm={10}>
                  <Input type="number" name="zip" id="zip" placeholder="What is your zip code?" value={zip} onChange={(e) => setZipCode(e.target.value)}  />
                </Col>
              </FormGroup>
              <FormGroup row>
                <Label htmlFor="propertyType">Property Type</Label><br />
                <Col sm={10}>
                <Input type="select" name="propertyType" id="propertyType" value={propertyType} onChange={(e) => setPropertyType(e.target.value)}  >
                  <option value="2">Apartment</option>
                  <option value="3">House</option>
                </Input>
                </Col>
              </FormGroup>
              <Button color="primary">Find Your Zip Code!</Button>
            </Form>
        </Row>
        <Row>
          Price - ${priceDisplay}
        </Row>
      </Container>
      <div id="googlemaps">
      <APIProvider apiKey={'AIzaSyBR4OUYOMC4iSFYayAdkfgjfc_itpVDGfA'} onLoad={() => console.log('Maps API has loaded.')}>
        <Map
            defaultZoom={10}
            center={ { lat: latitude, lng: longitude } }
            mapId='DEMO_MAP_ID'
            onCameraChanged={ (ev: MapCameraChangedEvent) =>
            console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)
            }>
        </Map>
          <AdvancedMarker
            position={{ lat: latitude, lng: longitude }}>
          </AdvancedMarker>
          {posits1.map( (posit) => (
            <AdvancedMarker
              position={ { lat: posit["lat"], lng: posit["lng"] } }
              price={posit.price}
              onClick={()=>setPriceDisplay(posit.price)}>
              <Pin background={'#1a2ae6'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
          {posits2.map( (posit) => (
            <AdvancedMarker
              position={ { lat: posit["lat"], lng: posit["lng"] } }
              price={posit.price}
              onClick={()=>setPriceDisplay(posit.price)}>
              <Pin background={'#1a2ae6'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
          {posits3.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ { lat: posit["lat"], lng: posit["lng"] } }
              price={posit.price}
              onClick={()=>setPriceDisplay(posit.price)}>
              <Pin background={'#3f4ef9'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
          {posits4.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ { lat: posit["lat"], lng: posit["lng"] } }
              price={posit.price}
              onClick={()=>setPriceDisplay(posit.price)}>
              <Pin background={'#8a93ff'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
          {posits5.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ { lat: posit["lat"], lng: posit["lng"] } }
              price={posit.price}
              onClick={()=>setPriceDisplay(posit.price)}>
              <Pin background={'#ADD8E6'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
        </APIProvider>
      </div>
  </div>
  );
}

export default App;
