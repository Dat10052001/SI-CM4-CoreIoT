import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Modal, 
  TextInput, TouchableOpacity, Alert, KeyboardAvoidingView,
  TouchableWithoutFeedback,
  Platform,
  Keyboard,  } from 'react-native';
import { Card, Button } from '@rneui/themed';
import Icon from 'react-native-vector-icons/FontAwesome5';

const initialFarms = {
  farm1: {
    name: 'nong trai dang mo',
    ID: 'SI001',
    address: 'ABC Street',
    plant: 'Paddy',
    status: 'Active',
  },
  farm2: {
    name: 'nong trai dong cua',
    ID: 'SI002',
    address: 'ABC Street',
    plant: 'Paddy',
    status: 'Inactive',
  },
};

const FarmCard = ({ ID, title, address, plant, status, onDelete }) => {
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

const Farms = props => {
  const [farms, setFarms] = useState(initialFarms);
  const [modalVisible, setModalVisible] = useState(false);
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);
  const [newFarm, setNewFarm] = useState('');
  const [reload, setReload] = useState(false);
  const [password, setPassword] = useState('');
  const [selectedFarmKey, setSelectedFarmKey] = useState(null);
  const [showID, setShowID] = useState();

  const openModal = () => {
    setShowID(`SI${String(Object.keys(farms).length + 1).padStart(3, '0')}`);
    setModalVisible(true);
  }

  const handleCreateFarm = () => {
    const newFarmKey = `farm${Object.keys(farms).length + 1}`;
    const newID = showID;
    setModalVisible(false);
    if(!newFarm.name.trim() || !newFarm.address.trim() || !newFarm.plant.trim()) {
      Alert.alert('Error', 'Please fill in all fields');
      setModalVisible(true);
      return;
    }
    setNewFarm({ ID: newID, name: '', address: '', plant: '', status: 'Inactive' });
    setFarms({ ...farms, [newFarmKey]: newFarm });
  };

  const handleDeleteFarm = (key) => {
    setSelectedFarmKey(key);
    setDeleteModalVisible(true);
  };

  const confirmDeleteFarm = () => {
    if (password === '123') {
      const updatedFarms = { ...farms };
      delete updatedFarms[selectedFarmKey];
      setFarms(updatedFarms);
      setDeleteModalVisible(false);
      setPassword('');
    } else {
      setPassword('');
      Alert.alert('Incorrect Password', 'The password you entered is incorrect.');
    }
  };

  const handleReload = () => {
    setReload(prev => !prev);
    setFarms({ ...initialFarms });
  };

  return (
    <View style={{ flex: 1 }}>
      <ScrollView contentContainerStyle={styles.container}>
        {Object.keys(farms).map((key, index) => (
          <View key={index} style={styles.cardContainer}>
            <FarmCard
              ID={farms[key].ID}
              title={farms[key].name}
              address={farms[key].address}
              plant={farms[key].plant}
              status={farms[key].status}
              onDelete={() => handleDeleteFarm(key)}
            />
          </View>
        ))}
        <View style={styles.buttonRow1}>
          <Button
            buttonStyle={styles.create_btn}
            title="CREATE"
            icon={<Icon name="plus" size={20} color="white" marginRight={15} />}
            onPress={openModal}
          />
          <Button
            buttonStyle={styles.reload_btn}
            title="RELOAD"
            icon={<Icon name="redo" size={20} color="white" marginRight={10} />}
            onPress={handleReload}
          />
        </View>
      </ScrollView>

      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={{ flex: 1 }}>
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>CREATE NEW FARM</Text>
            <Text style={styles.label_create}>ID: {showID}</Text>
            <Text style={styles.label_create}>Name</Text>
            <TextInput
              style={styles.input}
              placeholder="Address"
              value={newFarm.title}
              onChangeText={(text) => setNewFarm({ ...newFarm, name: text })}

            />
            <Text style={styles.label_create}>Address</Text>
            <TextInput
              style={styles.input}
              placeholder="Address"
              value={newFarm.address}
              onChangeText={(text) => setNewFarm({ ...newFarm, address: text })}
            />
            <Text style={styles.label_create}>Plant</Text>
            <TextInput
              style={styles.input}
              placeholder="Plant"
              value={newFarm.plant}
              onChangeText={(text) => setNewFarm({ ...newFarm, plant: text })}
            />
             <View style={styles.buttonRow}>
              <TouchableOpacity style={styles.modalButton} onPress={handleCreateFarm}>
                <Text style={styles.modalButtonText}>Create</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.modalButton} onPress={() => setModalVisible(false)}>
                <Text style={styles.modalButtonText}>Cancel</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
        </TouchableWithoutFeedback>
        </KeyboardAvoidingView>
      </Modal>

      <Modal
        animationType="slide"
        transparent={true}
        visible={deleteModalVisible}
        onRequestClose={() => setDeleteModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>CONFIRM DELETE</Text>
            <Text style={styles.label_create}>Type password to delete</Text>
            <TextInput
              style={styles.input}
              placeholder="Enter Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />
            <View style={styles.buttonRow}>
              <TouchableOpacity style={[styles.modalButton, {backgroundColor:'red'}]} onPress={confirmDeleteFarm}>
                <Text style={styles.modalButtonText}>Delete</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.modalButton} onPress={() => setDeleteModalVisible(false)}>
                <Text style={styles.modalButtonText}>Cancel</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    paddingVertical: 20,
  },
  cardContainer: {
    width: '80%',
    padding: 10,
  },
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
  view_button: {
    width: '85%',
    backgroundColor: '#059033',
    borderRadius: 10,
  },
  delete_button: {
    width: '80%',
    backgroundColor: 'red',
    borderRadius: 10,
  },
  create_btn: {
    backgroundColor: '#0074FF',
    borderRadius: 10,
    padding: 10,
    paddingRight: 20,
    paddingLeft: 20,
  },
  reload_btn: {
    backgroundColor: '#0074FF',
    borderRadius: 10,
    padding: 10,
    marginLeft: 20,
    paddingRight: 20,
    paddingLeft: 20,
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    width: '80%',
    backgroundColor: 'white',
    borderRadius: 15,
    padding: 20,
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    width: '100%',
    padding: 10,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
  },
  label_create: {
    alignSelf: 'flex-start',
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 15,
    marginBottom: 5,
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginTop: 10
  },
  buttonRow1: {
    flexDirection: 'row',
    justifyContent: 'center',
    width: '100%',
    marginTop: 20
  },
  modalButton: {
    backgroundColor: '#0074FF',
    padding: 10,
    borderRadius: 5,
    marginTop: 10,
    width: '48%',
    alignItems: 'center',
  },
  modalButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
});

export default Farms;