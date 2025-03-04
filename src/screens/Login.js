import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ImageBackground,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  TouchableWithoutFeedback,
  Keyboard,
  Alert,
} from 'react-native';
import { loginStyles } from '../../styles';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Login = props => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');  
  const [failedAttempts, setFailedAttempts] = useState(0);
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);
  const [countdown, setCountdown] = useState(60);

  useEffect(() => {
    const loadState = async () => {
      const storedFailedAttempts = await AsyncStorage.getItem('failedAttempts');
      const storedCountdown = await AsyncStorage.getItem('countdown');
      const storedIsButtonDisabled = await AsyncStorage.getItem('isButtonDisabled');

      if (storedFailedAttempts !== null) setFailedAttempts(parseInt(storedFailedAttempts));
      if (storedCountdown !== null) setCountdown(parseInt(storedCountdown));
      if (storedIsButtonDisabled !== null) setIsButtonDisabled(storedIsButtonDisabled === 'true');
    };

    loadState();
  }, []);

  useEffect(() => {
    let timer;
    if (failedAttempts >= 5) {
      setIsButtonDisabled(true);
      timer = setInterval(() => {
        setCountdown(prevCountdown => {
          if (prevCountdown <= 1) {
            clearInterval(timer);
            setIsButtonDisabled(false);
            setFailedAttempts(0);
            AsyncStorage.setItem('failedAttempts', '0');
            AsyncStorage.setItem('countdown', '60');
            AsyncStorage.setItem('isButtonDisabled', 'false');
            return 60;
          }
          AsyncStorage.setItem('countdown', (prevCountdown - 1).toString());
          return prevCountdown - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [failedAttempts]);

  const login = () => {
    if (phoneNumber === '123' && password === '123') {
      Alert.alert('Login Successful', 'Welcome to your farm!', [
        { text: 'OK', onPress: () => props.navigation.navigate('YOUR FARM') },
      ]);
    } else {
      setFailedAttempts(failedAttempts + 1);
      AsyncStorage.setItem('failedAttempts', (failedAttempts + 1).toString());
      if(failedAttempts >= 4) {
        Alert.alert('Login Locked', 'You have entered the wrong password 5 times. Please wait 1 minute before trying again.');
      } else {
        Alert.alert('Login Failed', 'Invalid phone number or password.', [
          { text: 'OK' },
        ]);
      }
    }
  };

  const signup = () => {
    props.navigation.navigate('SIGN UP, RESET PASSWORD');
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={{ flex: 1 }}>
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <ImageBackground 
          source={require("../assets/banner.jpg")} 
          style={loginStyles.background}
          resizeMode="cover"
        >
          <Text style={loginStyles.title}>WELCOME TO SMART IRRIGATION !</Text>
          
          <TextInput
            style={loginStyles.input}
            placeholder="Enter your phone number"
            keyboardType='numeric'
            value={phoneNumber}
            onChangeText={setPhoneNumber}
          />
          <TextInput
            style={loginStyles.input}
            placeholder="Enter your password"
            secureTextEntry={true}
            value={password}
            onChangeText={setPassword}
          />

          <TouchableOpacity onPress={login} disabled={isButtonDisabled}>
          <Text style=
          {[loginStyles.login_btn, isButtonDisabled && { backgroundColor: 'gray' }]}>
            {isButtonDisabled ? `Try again in ${countdown}s` : 'LOG IN'}
          </Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={signup}>
            <Text style={loginStyles.con_button}>SIGN UP OR RESET PASSWORD</Text>
          </TouchableOpacity>
        </ImageBackground>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
};

export default Login;