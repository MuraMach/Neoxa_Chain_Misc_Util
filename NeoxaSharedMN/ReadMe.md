For code improvements or suggestions please raise an issue.
For direct code upgrades please create a PR for peer review.




##Current Bounties##

Without the use of Taproot & SegWit:

1.) An creator output that has secret hidden data e.g. a game code that can only be retrieved by the person who holds the reveal or redemption key without revealing the creators private keys:: 2250 NEOX // Must have working code and example to test.
2.) A way to link OP_RETURN <83 Bytes of data> hex outputs to other future or past OP_RETURN outputs and be able to verify it on chain using a hash:: 8700 NEOX // Must have working code and example to test.
3.) OP_RETURN only supports 83 bytes of arbitrary data being pushed per tx/vout, the 83 byte limit is not an issue when calling multiple txids with arbitrary data to build code from a frond end parser but becomes harder to track as more and more code is added to be reused. To solve this we need to have an "ord" type protocol where we can push over 83 bytes in one push, one perhaps way is using similar methods to "ord" and port them to the Dash codebase using some other type of output script / OP / BTC&Dash Script. It must achieve the same outcome as an "ord" where over 83 bytes can be stored on chain forever in a script or imbued to sats or assets, IPFS is not to be used for this:: 22,500 NEOX // Must have working code and example to test.
