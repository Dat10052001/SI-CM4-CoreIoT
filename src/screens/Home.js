import React from 'react';
import { createDrawerNavigator } from '@react-navigation/drawer';
import Account from './Account';
import Setting from './Setting';
import Farms from './Farm';
import Icon from 'react-native-vector-icons/FontAwesome5';

const Drawer = createDrawerNavigator();

const Home = () => {
  return (
      <Drawer.Navigator initialRouteName="My Farm">
        <Drawer.Screen
          name="My Farm"
          component={Farms}
          options={{
            drawerLabel: 'My Farm',
            drawerIcon: ({ color, size }) => (
              <Icon name="home" color={color} size={size} />
            ),
          }}
        />
        <Drawer.Screen
          name="My Account"
          component={Account}
          options={{
            drawerLabel: 'My Account',
            drawerIcon: ({ color, size }) => (
              <Icon name="user" color={color} size={size} />
            ),
          }}
        />
        <Drawer.Screen
          name="Settings"
          component={Setting}
          options={{
            drawerLabel: 'Settings',
            drawerIcon: ({ color, size }) => (
              <Icon name="cog" color={color} size={size} />
            ),
          }}
        />
      </Drawer.Navigator>
  );
};

export default Home;