import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert, Modal, StyleSheet, ActivityIndicator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import NetInfo from '@react-native-community/netinfo';
import Start from './src/screens/Start';
import Login from './src/screens/Login';
import Home from './src/screens/Home';
import SignUp from './src/screens/SignUp';
import 'react-native-reanimated';

const App = () => {
  const Stack = createStackNavigator();
  const [isConnected, setIsConnected] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [isLoading, setIsLoading] = useState(false);


  useEffect(() => {
    const checkConnection = () => {
      NetInfo.fetch().then(state => {
        if (!state.isConnected) {
          setIsConnected(false);
          setModalVisible(true);
        } else {
          setIsConnected(true);
          setModalVisible(false);
        }
      });
    };

    const interval = setInterval(checkConnection, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleReconnect = () => {
    setIsLoading(true);
    setTimeout(() => {
      NetInfo.fetch().then(state => {
        setIsLoading(false);
        if (state.isConnected) {
          setIsConnected(true);
          setModalVisible(false);
        } else {
          Alert.alert('No Connection', 'Please check your internet connection and try again.');
        }
      });
    }, 10000);
  };

  return (
    <View style={{ flex: 1 }}>
      <NavigationContainer>
        <Stack.Navigator>
          {/* <Stack.Screen name="STARTING" component={Start} /> */}
          <Stack.Screen name="LOGIN" component={Login} />
          <Stack.Screen name="SIGN UP, RESET PASSWORD" component={SignUp} />
          <Stack.Screen name="HOME" component={Home} options={{ headerLeft: null }} />
        </Stack.Navigator>
      </NavigationContainer>
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => {
          setModalVisible(!modalVisible);
        }}
      >
        <View style={styles.centeredView}>
          <View style={styles.modalView}>
            <Text style={styles.modalText}>Connection Lost 🚫</Text>
            {isLoading ? (
              <ActivityIndicator size="large" color="#059033" />
            ) : (
              <Button color="#059033" title="Reconnect" onPress={handleReconnect} />
            )}
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22,
  },
  modalView: {
    margin: 20,
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 35,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalText: {
    marginBottom: 15,
    textAlign: 'center',
    fontSize: 20,
    color: 'red',
  },
});

export default App;