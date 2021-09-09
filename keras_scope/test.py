import tensorflow as tf
from keras_scope.datasets.gsd_outcome_dataset import get_gsd_outcome_dataset
from keras_scope.metrics import f1_m
from keras_scope.model import get_model

precision = tf.keras.metrics.Precision()
recall = tf.keras.metrics.Recall()


def test(model_path, label_file_path, imaging_dataset_path, outcome, channels, desired_shape):
    test_ratio = 1
    batch_size = 200

    _, test_dataset = get_gsd_outcome_dataset(label_file_path, imaging_dataset_path,
                                              outcome, channels,
                                              desired_shape, test_ratio, batch_size)

    model = get_model(width=desired_shape[0], height=desired_shape[1], depth=desired_shape[2], channels=len(channels))

    model.compile(
        metrics=["acc", "AUC", f1_m, precision, recall],
    )

    model.load_weights(model_path)
    result = model.evaluate(test_dataset)

    print(dict(zip(model.metrics_names, result)))
    return dict(zip(model.metrics_names, result))


if __name__ == '__main__':
    model_path = '/home/hendrik/jk/output/keras_scope/20210821-104512/3d_image_classification.h5'
    label_file_path = '/mnt/data/hendrik/jk/scope_data/joined_anon_outcomes_2015_2016_2017_2018_df.xlsx'
    imaging_dataset_path = '/mnt/data/hendrik/jk/scope_data/test_noGT_pmaps_15-19_dataset_with_combined_mRS_90_days.npz'
    outcome = "combined_mRS_0-2_90_days"
    channels = [0, 1, 2, 3]
    desired_shape = (46, 46, 46)

    test(model_path, label_file_path, imaging_dataset_path, outcome, channels, desired_shape)
