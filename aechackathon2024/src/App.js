import './App.css';
import {APIProvider, Map, MapCameraChangedEvent, AdvancedMarker, Pin } from '@vis.gl/react-google-maps';
import  ZipToGeo  from './utilities/ziptogeo'
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
  const [ zip, setZipCode ] = useState('90017')
  const [ propertyType, setPropertyType ] = useState('')
  const [ latitude, setLatitude ] = useState(34.052913)
  const [ longitude, setLongitude ] = useState(-118.264340)

  const [  posits90, setPosits90  ] = useState([])

  const [  posits80, setPosits80  ] = useState([])

  const [  posits70, setPosits70  ] = useState([])
  
  const submit = async (e) =>{
    e.preventDefault();

    let lat, lng;
    ({lat, lng} =  ZipToGeo(zip));
    setLatitude(lat)
    setLongitude(lng)

    const response = await fetch('http://127.0.0.1:5000/rank-areas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        zip: zip, 
        price: price, 
        propertyType: propertyType
      })
    });

    const data = await response.json();
    if (data.status === 'success') {
      let posits90arr = []
      let posits80arr = []
      let posits70arr = []

      //const rankedAreas = data.data;
      const rankedAreas = [

        {area: "Area 1", "similarity_score": 90, lat: 34.039378, lng: -118.266300 },
        {area: "Area 2", "similarity_score": 85, lat: 34.028331, lng: -118.354338 },
        {area: "Area 3", "similarity_score": 80, lat: 34.028887, lng: -118.317183  },
        {area: "Area 4", "similarity_score": 75, lat: 34.049841, lng: -118.338460 },
      ]

      for (let i = 0; i < rankedAreas.length; i++){
        let obj = { key: i + 1, location: {lat: rankedAreas[i].lat, lng: rankedAreas[i].lng}}
        if (rankedAreas[i]["similarity_score"] >= 90){
          posits90arr.push(obj)
        } else if (rankedAreas[i]["similarity_score"]  >= 80 && rankedAreas[i]["similarity_score"]  < 90){
          posits80arr.push(obj)
        } else if (rankedAreas[i]["similarity_score"]  >= 70 && rankedAreas[i]["similarity_score"]  < 80){
          posits70arr.push(obj)
        }
      }

      // Update the positions based on the API response
      setPosits90(posits90arr)
      setPosits80(posits80arr)
      setPosits70(posits70arr)

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
          {posits90.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ posit.location }>
              <Pin background={'#002366'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
          {posits80.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ posit.location }>
              <Pin background={'#2A52BE'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
          {posits70.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ posit.location }>
              <Pin background={'#ADD8E6'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
        </APIProvider>
      </div>
  </div>
  );
}

export default App;
