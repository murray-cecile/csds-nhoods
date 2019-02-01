echo "hello world" | tee hello.txt

##################
# in hello.submit
##################

universe = vanilla

# Executable and inputs
executable              = /home/cmmurray/hello.sh 
initialdir              = /stash/user/cmmurray/

# Save your work.
ShouldTransferFiles     = YES
when_to_transfer_output = ON_EXIT

log    = /stash/user/cmmurray/post.$(Cluster).{}.log
error  = /stash/user/cmmurray/post.$(Cluster).{}.err
output = /stash/user/cmmurray/post.$(Cluster).{}.out

transfer_output_files  = hello.txt

queue