import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Start from './src/screens/Start';
import Login from './src/screens/Login';
import HomeScreen from './src/screens/HomeScreen';
import Control from './src/screens/Control';
import Data from './src/screens/Data';
import OpenDoor from './src/screens/OpenDoor';

const App = () => {
  const Stack = createStackNavigator();
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="STARTING" component={Start} />
        <Stack.Screen name="LOGIN" component={Login} />
        <Stack.Screen name="YOUR FARM" component={HomeScreen} />
        <Stack.Screen name="CONTROL" component={Control} />
        <Stack.Screen name="DATA" component={Data} />
        <Stack.Screen name="OTHERSS" component={OpenDoor} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;