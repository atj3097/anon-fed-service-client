from zksk import Secret, DLRep, Circuit

class ModelUpdateCircuit(Circuit):
    def __init__(self, updated_params, old_params, threshold):
        # Define the inputs to the circuit
        self.updated_params = updated_params
        self.old_params = old_params
        self.threshold = threshold

        # Define the outputs of the circuit
        self.valid_update = Secret()

        # Define the internal variables of the circuit
        self.diff = [Secret() for _ in range(len(updated_params))]
        self.exceeded_threshold = Secret()

        # Call the superclass constructor
        super().__init__()

    def evaluate(self):
        # Compute the difference between the updated and old parameters
        for i in range(len(self.updated_params)):
            self.diff[i].assign(self.updated_params[i] - self.old_params[i])

        # Compute whether the update exceeds the threshold
        self.exceeded_threshold.assign(sum(self.diff) > self.threshold)

        # Compute whether the update is valid
        valid = True
        for i in range(len(self.updated_params)):
            # Check that the updated parameter is greater than the old parameter
            valid &= self.updated_params[i] > self.old_params[i]

            # Check that the difference is equal to the updated parameter minus the old parameter
            valid &= self.diff[i] == self.updated_params[i] - self.old_params[i]

        # Check that the update does not exceed the threshold
        valid &= not self.exceeded_threshold

        # Assign the output
        self.valid_update.assign(valid)


def generate_proof(updated_params, old_params, threshold):
    # Define the circuit
    circuit = ModelUpdateCircuit(updated_params, old_params, threshold)

    # Define the inputs and witness values
    inputs = {
        "updated_params": [DLRep(param, curve=curve) for param in updated_params],
        "old_params": [DLRep(param, curve=curve) for param in old_params],
        "threshold": threshold,
    }
    witness = {
        "valid_update": circuit.valid_update,
        "diff": circuit.diff,
        "exceeded_threshold": circuit.exceeded_threshold,
    }

    # Generate the proof
    try:
        proving_key = PrivateKey.random(circuit)
        public_key = proving_key.get_vk()
        proof = proving_key.prove(inputs, witness)
    except ProvingError:
        return None

    # Serialize the proof and public key
    serialized_proof = serialize(proof)
    serialized_public_key = serialize(public_key)

    # TODO: Return the serialized proof and public key
    return serialized_proof, serialized_public_key

# Create the verification key and proving key using the ProvingScheme class
proving_key, verification_key = utils.generate_zksk_keys(ModelUpdateCircuit)

def verify_proof(updated_params, old_params, threshold, proof):
    # Create the public inputs and assign the values
    public_inputs = [updated_params, old_params, threshold]

    # Create the witness and assign the values
    witness = [updated_params, old_params, threshold]

    # Create an instance of the circuit
    circuit = ModelUpdateCircuit(updated_params, old_params, threshold)

    # Verify the proof using the verify method of the proof object
    return proof.verify(circuit, public_inputs, verification_key)
