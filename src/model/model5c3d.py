import tensorflow as tf
import tf_helpers

SEED = 22

def encode_rad(input, n_labels, do=True):
    #do is dropouts, true for training, false for testing
    l = tf_helpers.get_radian_conv("conv1",input,3,3,32)
    l = tf_helpers.get_radian_conv("conv2",l,3,3,32)
    l = tf_helpers.get_radian_pool(l,1)
    l = tf_helpers.get_radian_conv("conv3",l,3,3,64)
    l = tf_helpers.get_radian_conv("conv4",l,3,3,64)
    l = tf_helpers.get_radian_pool(l,2)
    l = tf_helpers.get_radian_conv("conv5",l,3,3,128)
    l = tf_helpers.get_radian_conv("conv6",l,3,3,128)
    l = tf_helpers.get_radian_pool(l,3)
    l = tf_helpers.get_radian_conv("conv7",l,3,3,256)
    l = tf_helpers.get_radian_conv("conv8",l,3,3,256)
    l = tf_helpers.get_radian_pool(l,4)
    l = tf_helpers.get_radian_conv("conv9",l,3,3,512)
    l = tf_helpers.get_radian_conv("conv10",l,3,3,512)
    l = tf_helpers.get_radian_pool(l,5)
    l = tf_helpers.get_radian_conv("conv11",l,2,2,1024)
    l = tf_helpers.get_radian_conv("conv12",l,2,2,1024)
    l = tf_helpers.get_radian_pool(l,6)
    l = tf_helpers.get_dense_layer_relu("dense1",l,4096)
    if do:
       l = tf.nn.dropout(l,.5)
    l = tf_helpers.get_dense_layer_relu("dense2",l,4096)
    if do:
       l = tf.nn.dropout(l,.5)
    l = tf_helpers.get_softmax_linear_layer("softmax_linear",l,n_labels)
    return l

def encoding_img(input, n_labels, do=True, batch_size):
    with tf.variable_scope('conv1') as scope:
    kernel = _variable_with_weight_decay('weights',
                                         shape=[5, 5, 3, 64],
                                         stddev=5e-2,
                                         wd=0.0)
    conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')
    biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.0))
    bias = tf.nn.bias_add(conv, biases)
    conv1 = tf.nn.relu(bias, name=scope.name)
    _activation_summary(conv1)

  # pool1
  pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1],
                         padding='SAME', name='pool1')
  # norm1
  norm1 = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,
                    name='norm1')

  # conv2
  with tf.variable_scope('conv2') as scope:
    kernel = _variable_with_weight_decay('weights',
                                         shape=[5, 5, 64, 64],
                                         stddev=5e-2,
                                         wd=0.0)
    conv = tf.nn.conv2d(norm1, kernel, [1, 1, 1, 1], padding='SAME')
    biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.1))
    bias = tf.nn.bias_add(conv, biases)
    conv2 = tf.nn.relu(bias, name=scope.name)
    _activation_summary(conv2)

  # norm2
  norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,
                    name='norm2')
  # pool2
  pool2 = tf.nn.max_pool(norm2, ksize=[1, 3, 3, 1],
                         strides=[1, 2, 2, 1], padding='SAME', name='pool2')

  # local3
  with tf.variable_scope('local3') as scope:
    # Move everything into depth so we can perform a single matrix multiply.
    reshape = tf.reshape(pool2, [batch_size, -1])
    dim = reshape.get_shape()[1].value
    weights = _variable_with_weight_decay('weights', shape=[dim, 384],
                                          stddev=0.04, wd=0.004)
    biases = _variable_on_cpu('biases', [384], tf.constant_initializer(0.1))
    local3 = tf.nn.relu(tf.matmul(reshape, weights) + biases, name=scope.name)
    _activation_summary(local3)

  # local4
  with tf.variable_scope('local4') as scope:
    weights = _variable_with_weight_decay('weights', shape=[384, 192],
                                          stddev=0.04, wd=0.004)
    biases = _variable_on_cpu('biases', [192], tf.constant_initializer(0.1))
    local4 = tf.nn.relu(tf.matmul(local3, weights) + biases, name=scope.name)
    _activation_summary(local4)

  # softmax, i.e. softmax(WX + b)
  with tf.variable_scope('softmax_linear') as scope:
    weights = _variable_with_weight_decay('weights', [192, n_labels],
                                          stddev=1/192.0, wd=0.0)
    biases = _variable_on_cpu('biases', [n_labels],
                              tf.constant_initializer(0.0))
    softmax_linear = tf.add(tf.matmul(local4, weights), biases, name=scope.name)
    _activation_summary(softmax_linear)

  return softmax_linear

    # l = tf_helpers.get_conv("conv1",input,3,3,32)
    # l = tf_helpers.get_pool_and_lrn(l,1)
    # l = tf_helpers.get_conv("conv2",input,3,3,64)
    # l = tf_helpers.get_pool_and_lrn(l,2)
    # l = tf_helpers.get_conv("conv3",input,3,3,128)
    # l = tf_helpers.get_pool_and_lrn(l,3)
    # l = tf_helpers.get_conv("conv4",input,3,3,256)
    # l = tf_helpers.get_pool_and_lrn(l,4)
    # l = tf_helpers.get_conv("conv5",input,3,3,512)
    # l = tf_helpers.get_pool_and_lrn(l,5)
    # l = tf_helpers.get_dense_layer_relu("dense1",l,256)
    # if do:
    #    l = tf.nn.dropout(l,.5)
    # l = tf_helpers.get_dense_layer_relu("dense2",l,128)
    # if do:
    #    l = tf.nn.dropout(l,.5)
    # l = tf_helpers.get_softmax_linear_layer("softmax_linear",l,n_labels)
    # return l
def _variable_on_cpu(name, shape, initializer):
  """Helper to create a Variable stored on CPU memory.
  Args:
    name: name of the variable
    shape: list of ints
    initializer: initializer for Variable
  Returns:
    Variable Tensor
  """
  with tf.device('/cpu:0'):
    dtype = tf.float32
    var = tf.get_variable(name, shape, initializer=initializer, dtype=dtype)
  return var


def _variable_with_weight_decay(name, shape, stddev, wd):
  """Helper to create an initialized Variable with weight decay.
  Note that the Variable is initialized with a truncated normal distribution.
  A weight decay is added only if one is specified.
  Args:
    name: name of the variable
    shape: list of ints
    stddev: standard deviation of a truncated Gaussian
    wd: add L2Loss weight decay multiplied by this float. If None, weight
        decay is not added for this Variable.
  Returns:
    Variable Tensor
  """
  dtype = tf.float32
  var = _variable_on_cpu(
      name,
      shape,
      tf.truncated_normal_initializer(stddev=stddev, dtype=dtype))
  if wd is not None:
    weight_decay = tf.mul(tf.nn.l2_loss(var), wd, name='weight_loss')
    tf.add_to_collection('losses', weight_decay)
  return var
