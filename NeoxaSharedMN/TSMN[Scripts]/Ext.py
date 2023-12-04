def multisig_masternode_script(user_signature, whitelisted_users, current_block_height, lock_until_block_height,
                               masternode_proposal_flag, user_masternode_proposal, proposal_id, creator_address,
                               proposal_comments, proposal_metadata, proposal_expiry_blocks,
                               proposal_rejection_threshold, voting_start_block_height, masternode_operators,
                               operator_opt_out_flag, operator_redemption_signature, redemption_block_height,
                               operator_signature):
    script = []

    # Check if the provided signature matches a whitelisted participant
    script.extend([user_signature] + whitelisted_users + [f"{len(whitelisted_users)} OP_CHECKMULTISIGVERIFY"])

    # Check if the collateral deposit is locked for masternode
    script.extend([f"{current_block_height} {lock_until_block_height} OP_LE OP_VERIFY"])

    # Masternode proposal submission logic
    script.extend([masternode_proposal_flag, "OP_IF"])
    # User's masternode proposal
    script.extend([user_masternode_proposal, f"{user_signature} OP_CHECKSIGVERIFY"])
    # Masternode proposal data
    script.extend([f"\"Masternode Proposal Title\" \"Masternode Proposal Description\" 1000 {proposal_id} {creator_address} " 
                   f"\"{proposal_comments}\" \"Pending\" \"{proposal_metadata}\" {proposal_expiry_blocks} "
                   f"{proposal_rejection_threshold}"])
    # Proposal locking once voting starts
    script.extend([f"{voting_start_block_height} {current_block_height} OP_LE OP_VERIFY"])
    # Additional custom voting logic for masternode proposals
    script.extend(masternode_operators)
    # Count the number of masternode operator votes
    script.extend(["0 OP_TOALTSTACK"])
    script.extend([f"{len(masternode_operators)} OP_ADD"])
    # Dynamic voting threshold calculation
    script.extend(["OP_2 OP_DIV OP_TOALTSTACK OP_DUP OP_NUMEQUALVERIFY OP_FROMALTSTACK OP_NUMEQUALVERIFY"])
    # Proposal expiry
    script.extend([f"{current_block_height} {proposal_expiry_blocks} OP_SUB OP_GREATERTHAN OP_NOTIF"])
    script.extend(["\"Expired\" OP_RETURN OP_ENDIF"])
    # Masternode operators can opt-out or be removed
    script.extend([operator_opt_out_flag, "OP_IF"])
    script.extend(["\"Rejected\" OP_RETURN OP_ENDIF"])
    # Proposal voting timeframe
    script.extend([f"{current_block_height} {voting_start_block_height} OP_SUB 1440 OP_GREATERTHAN OP_NOTIF"])
    script.extend(["\"Rejected\" OP_RETURN OP_ENDIF"])
    # Redemption logic for masternode operators
    script.extend([operator_redemption_signature, f"{current_block_height} {redemption_block_height} OP_LE OP_VERIFY"])
    script.extend([f"{operator_signature} OP_CHECKSIGVERIFY", "\"Redemption\" OP_RETURN"])
    script.extend(["OP_ENDIF"])
    # Additional logic to prevent double voting by operators
    script.extend(["OP_HASH160", "<hash_of_operator_pubkey> OP_EQUALVERIFY OP_CHECKSIGVERIFY"])
    # Additional logic for user-initiated opt-out and collateral retrieval
    script.extend([operator_opt_out_flag, "OP_IF"])
    script.extend([f"{current_block_height} {redemption_block_height} OP_LE OP_VERIFY"])
    script.extend([f"{user_signature} OP_CHECKSIGVERIFY", "\"User Opt-Out\" OP_RETURN"])
    script.extend(["OP_ENDIF"])
    script.extend([f"{creator_address} {whitelisted_users[0]} OP_EQUALVERIFY"])
    script.extend([f"\"{proposal_metadata}\" OP_RETURN"])
    script.extend([f"\"Comments: {proposal_comments}\" OP_RETURN"])

    return " ".join(script)
