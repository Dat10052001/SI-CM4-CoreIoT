import React from 'react';
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
} from 'react-native';
import styles from '../../styles';

const Login = props => {
  const login = () => {
    props.navigation.navigate('YOUR FARM');
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={{ flex: 1 }}>
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <ImageBackground 
          source={require("../assets/banner.jpg")} 
          style={styles.background}
          resizeMode="cover"
        >
          <Text style={styles.title}>WELCOME TO SMART IRRIGATION</Text>
          
          <TextInput style={styles.input} placeholder="Enter your phone number" />
          <TextInput style={styles.input} placeholder="Enter your password" secureTextEntry={true} />

          <TouchableOpacity onPress={login}>
            <Text style={styles.login_btn}>LOG IN</Text>
          </TouchableOpacity>

          <TouchableOpacity>
            <Text style={styles.con_button}>Don't have an account or Forgot password</Text>
          </TouchableOpacity>
        </ImageBackground>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
};

export default Login;