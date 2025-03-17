import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card, Button } from '@rneui/themed';

const FarmCard = ({ ID, title, address, plant, status, onDelete, onView }) => {
  return (
    <Card containerStyle={styles.card}>
      <Card.Title style={styles.cardTitle}>{title}</Card.Title>
      <Card.Divider />
      <View style={styles.user}>
        <Text style={styles.label}>ID: <Text style={styles.name}>{ID}</Text></Text>
        <Text style={styles.label}>ADDRESS: <Text style={styles.name}>{address}</Text></Text>
        <Text style={styles.label}>PLANT: <Text style={styles.name}>{plant}</Text></Text>
        <Text style={styles.label}>STATUS: <Text style={[styles.name, status === 'Active' ? styles.active : styles.inactive]}>{status}</Text></Text>
      </View>
      <View style={styles.buttonRow}>
        <Button
          buttonStyle={styles.view_button}
          title="VIEW"
          onPress={onView}
        />
        <Button
          buttonStyle={styles.delete_button}
          title="DELETE"
          onPress={onDelete}
        />
      </View>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    borderRadius: 15,
    padding: 20,
    backgroundColor: '#fff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 5,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  user: {
    marginVertical: 10,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  name: {
    fontSize: 16,
    fontWeight: 'normal',
  },
  active: {
    color: 'green',
    fontWeight: 'bold',
  },
  inactive: {
    color: 'red',
    fontWeight: 'bold',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginTop: 10,
  },
  view_button: {
    width: '82%',
    backgroundColor: '#059033',
    borderRadius: 10,
  },
  delete_button: {
    width: '75%',
    backgroundColor: 'red',
    borderRadius: 10,
    marginLeft: 8,
  },
});

export default FarmCard;