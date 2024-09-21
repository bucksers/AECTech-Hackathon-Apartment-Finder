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

  const [  posits, setPosits  ] = useState([
    {key: '1', location: { lat: 34.039378, lng: -118.266300  }},
    {key: '2', location: { lat: 34.028331, lng: -118.354338  }},
    {key: '3', location: { lat: 34.028887, lng: -118.317183  }},
    {key: '4', location: { lat: 34.049841, lng: -118.338460  }}
  ])
  
  const submit = (e) =>{
    e.preventDefault();

    let lat, lng;
    ({lat, lng} =  ZipToGeo(zip));
    setLatitude(lat)
    setLongitude(lng)

    let zipNumber = parseInt(zip);

    setPosits([
    {key: '1', location: ZipToGeo((zipNumber - 2).toString()) },
    {key: '2', location: ZipToGeo((zipNumber - 1).toString()) },
    {key: '3', location: ZipToGeo((zipNumber + 1).toString()) },
    {key: '4', location: ZipToGeo((zipNumber + 2).toString()) }
    ])

  }


  return (<div className="App">
      <h1 id ="title">Find Your Apartment</h1>
      <Container >
        <Row>
          <Col></Col>
          <Col xl={3}>
            <Form className="p-4" id="initial-form" onSubmit={submit} >
              <FormGroup>
                <Label htmlFor="price">Price</Label>
                <Input type="number" name="price" id="price" placeholder="Enter your price" value={price} onChange={(e) => setPrice(e.target.value)} />
              </FormGroup>
              <FormGroup>
                <Label htmlFor="zip">Zip Code</Label>
                <Input type="number" name="zip" id="zip" placeholder="What is your zip code?" value={zip} onChange={(e) => setZipCode(e.target.value)}  />
              </FormGroup>
              <FormGroup>
                <Label htmlFor="propertyType">Property Type</Label><br />
                <Input type="select" name="propertyType" id="propertyType" value={propertyType} onChange={(e) => setPropertyType(e.target.value)}  >
                  <option value="2">Apartment</option>
                  <option value="3">House</option>
                </Input>
              </FormGroup>
              <Button color="primary">Find Your Apartment!</Button>
            </Form>
          </Col>
          <Col></Col>
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
          {posits.map( (posit) => (
            <AdvancedMarker
              key={ posit.key }
              position={ posit.location }>
              <Pin background={'#FBBC04'} glyphColor={'#000'} borderColor={'#000'} />
            </AdvancedMarker>
          ))}
        </APIProvider>
      </div>
  </div>
  );
}

export default App;
