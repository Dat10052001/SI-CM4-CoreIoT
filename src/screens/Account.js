import React from 'react';
import { View, Text, Button, Alert } from 'react-native';
import { CommonActions } from '@react-navigation/native';

const Account = ({ navigation }) => {
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
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Your Account</Text>
      <Button title="Log Out" onPress={handleLogout} />
    </View>
  );
};

export default Account;