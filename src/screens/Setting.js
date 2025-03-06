import React from 'react';
import { 
  View, Text, Alert, StyleSheet, Keyboard, Platform, TextInput,
  TouchableWithoutFeedback, TouchableOpacity, KeyboardAvoidingView 
} from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome5';
import { CommonActions } from '@react-navigation/native';
import { signupStyles } from '../../styles';

const Setting = ({ navigation }) => {
  const handleResetPassword = () => {
    // Handle password reset logic here
  };

  const handleLogout = () => {
    Alert.alert(
      'Log Out',
      'Are you sure you want to log out?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Log Out',
          onPress: () => {
            navigation.dispatch(
              CommonActions.reset({
                index: 0,
                routes: [{ name: 'LOGIN' }],
              })
            );
          },
        },
      ],
      { cancelable: false }
    );
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={{ flex: 1 }}>
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View style={{ flex: 1 }}>
          <View style={styles.section}>
            <Text style={signupStyles.title}>RESET PASSWORD</Text>
            <TextInput style={[signupStyles.input, signupStyles.inputEnabled]} placeholder="Currnet Password" secureTextEntry={true} />
            <TextInput style={[signupStyles.input, signupStyles.inputEnabled]} placeholder="New Password" secureTextEntry={true} />
            <TextInput style={[signupStyles.input, signupStyles.inputEnabled]} placeholder="Confirm new password" secureTextEntry={true} />
            <TouchableOpacity onPress={handleResetPassword}>
              <Text style={signupStyles.reset_btn1}>Reset Password</Text>
            </TouchableOpacity>
          </View>

          <View style={styles.section}>
            <Text style={signupStyles.title}>LOG OUT</Text>
            <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
              <View style={styles.logoutButtonContent}>
                <Text style={styles.logoutButtonText}>Log Out</Text>
                <Icon name="sign-out-alt" color={'white'} size={20} style={styles.logoutButtonIcon} />
              </View>
            </TouchableOpacity>
          </View>
        </View>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  section: {
    flex: 1,
    //alignItems: 'center',
    //justifyContent: 'center',
    marginLeft: '10%',
    marginTop: '15%',
  },
  logoutButton: {
    backgroundColor: '#0074ff',
    padding: 15,
    borderRadius: 15,
    marginTop: 15,
    width: '50%',
    marginLeft: '20%',
  },
  logoutButtonText: {
    color: 'white',
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: 18,
  },
  logoutButtonContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoutButtonIcon: {
    marginLeft: 10,
  },
});

export default Setting;